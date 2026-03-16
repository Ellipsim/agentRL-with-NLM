(define (problem problem_1)

(:domain BLOCKS)

(:objects
	obj0 obj1 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(handempty)
	(ontable obj0)
	(ontable obj1)
)

(:goal (and
	(on obj0 obj1)
))
)