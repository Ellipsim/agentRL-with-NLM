

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b9)
(on b7 b1)
(on b8 b6)
(on b9 b7)
(on b10 b8)
(clear b4)
(clear b10)
)
(:goal
(and
(on b3 b9)
(on b4 b10)
(on b6 b8)
(on b9 b6))
)
)


