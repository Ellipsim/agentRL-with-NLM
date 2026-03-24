(define (problem problem_3)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj9)
	(clear obj10)
	(clear obj13)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj3)
	(on obj7 obj5)
	(on obj8 obj6)
	(on obj9 obj7)
	(on obj10 obj8)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj4)
	(ontable obj11)
)

(:goal (and
	(on obj0 obj1)
	(on obj1 obj2)
	(on obj2 obj3)
	(on obj3 obj10)
	(on obj5 obj4)
	(on obj7 obj5)
	(on obj8 obj13)
	(on obj9 obj7)
	(on obj10 obj12)
	(on obj12 obj11)
	(on obj13 obj9)
))
)