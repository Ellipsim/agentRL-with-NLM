

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b10)
(on b3 b9)
(on b4 b7)
(on b5 b1)
(on b6 b3)
(on b7 b2)
(on b8 b4)
(on b9 b5)
(ontable b10)
(clear b6)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b3 b5)
(on b5 b10)
(on b6 b9)
(on b8 b2)
(on b10 b1))
)
)


