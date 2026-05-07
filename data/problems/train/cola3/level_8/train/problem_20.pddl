

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b5)
(ontable b3)
(ontable b4)
(on b5 b6)
(on b6 b9)
(ontable b7)
(on b8 b7)
(on b9 b4)
(clear b1)
(clear b2)
(clear b8)
)
(:goal
(and
(on b1 b9)
(on b2 b1)
(on b3 b4)
(on b5 b2)
(on b6 b5)
(on b7 b8)
(on b8 b3)
(on b9 b7))
)
)


