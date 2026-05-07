

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b2)
(ontable b4)
(ontable b5)
(on b6 b4)
(ontable b7)
(on b8 b1)
(on b9 b3)
(clear b5)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b1)
(on b3 b6)
(on b5 b2)
(on b6 b5)
(on b8 b7)
(on b9 b3))
)
)


