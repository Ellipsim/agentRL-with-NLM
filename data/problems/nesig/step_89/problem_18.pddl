(define (problem problem_18)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(clear obj5)
	(clear obj8)
	(clear obj10)
	(clear obj14)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj10 obj9)
	(on obj12 obj11)
	(on obj13 obj12)
	(on obj14 obj13)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj5)
	(ontable obj6)
	(ontable obj9)
	(ontable obj11)
)

(:goal (and
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj10 obj14)
	(on obj12 obj11)
	(on obj14 obj5)
))
)