

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b7)
(on b3 b2)
(ontable b4)
(ontable b5)
(on b6 b10)
(on b7 b1)
(on b8 b3)
(on b9 b8)
(on b10 b4)
(clear b5)
(clear b9)
)
(:goal
(and
(on b2 b6)
(on b3 b4)
(on b5 b8)
(on b7 b1)
(on b9 b5)
(on b10 b2))
)
)


