

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b9)
(ontable b2)
(on b3 b7)
(on b4 b2)
(ontable b5)
(on b6 b8)
(ontable b7)
(on b8 b1)
(on b9 b4)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b3 b5)
(on b5 b1)
(on b6 b9)
(on b7 b4)
(on b8 b2)
(on b9 b8))
)
)


