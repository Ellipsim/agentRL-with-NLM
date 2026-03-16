

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b5)
(ontable b4)
(on b5 b8)
(on b6 b7)
(ontable b7)
(on b8 b2)
(on b9 b3)
(clear b4)
(clear b6)
(clear b9)
)
(:goal
(and
(on b4 b8)
(on b5 b4)
(on b6 b3)
(on b7 b1))
)
)


