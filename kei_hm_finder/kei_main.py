import excel_reader, timeit, gauss_processor, kei_hm, calc_wirt

def find_hm(kei_index, kei, rank, gcode):
    knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gcode)
    if wirt_num != rank:
        return False
    gnr = kei_hm.generator_finder(wirt_num, kei)
    hm_check, gen_set = kei_hm.homomorphism_finder(seed_strand_set, knot_dict, gnr, kei)
    if hm_check:
        print("A surjective homomorphism to", kei_index, "is found.")
        print("Mapping:", gen_set)
        print()
        return True
    else:
        return False
        print("Did not find any surjective homomorphism to", kei_index)

def kei_hm_main():
    kei_dict = excel_reader.kei_dict_creator("kei_database.xlsx")
    print("Welcome to kei homomorphism finder, Please choose an option from the following,")
    option = input("Enter 1 if you would like to input the Gauss code of a single knot, 2 if you would like to input an Excel file: ")
    while option!='1' and option!='2':
        option = input("Please enter a valid option (1 or 2):")

    if option == '1':
        raw_gcode = input(
            "Please Enter the gauss code of the knot as a sequence of integers. Use any separation characters you like: ")
        gcode = gauss_processor.process_gauss_code(raw_gcode)
        knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gcode)
        print("Wirtinger number:", wirt_num)
        print("Seed strand set used to color the knot:", seed_strand_set)
        print("Knot dictionary:", knot_dict,"\n")
        option2 = input("Enter 1 if you would like to test the knot on a single kei, 2 if you would like to test it on all finite keis under order 36: ")

        while option2 != '1' and option2 != '2':
            option2 = input("Please enter a valid option (1 or 2): ")

        if option2 == '1':
            kei_index = input("Please enter the RIG index of the kei (you can find them under kei_database.xlsx): ")
            while kei_index not in kei_dict.keys():
                kei_index = input("Please enter a valid RIG index (you can find them under kei_database.xlsx): ")
            find_hm(kei_index, kei_dict[kei_index][0], kei_dict[kei_index][1], gcode)
        else:
            no_hm = ""
            for kei_index in kei_dict.keys():
                if not find_hm(kei_index, kei_dict[kei_index][0],kei_dict[kei_index][1], gcode):
                    no_hm += str(kei_index) +", "
            print("Did not find any surjective homomorphism to:\n", no_hm)

    else:
        input_file = input("Enter the input file path (including directory and extension): ")
        start = timeit.default_timer()
        excel_reader.excel_qnd_main(input_file)
        print("Run time: ", (timeit.default_timer() - start)//3600, "hours,",(timeit.default_timer() - start)%3600//60,"minutes,", (timeit.default_timer() - start)%3600%60, "seconds.")
    print("The program will terminate now.")


kei_hm_main()
