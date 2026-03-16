

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b9)
(on b3 b7)
(on b4 b3)
(on b5 b6)
(on b6 b4)
(on b7 b10)
(ontable b8)
(on b9 b5)
(ontable b10)
(clear b1)
(clear b8)
)
(:goal
(and
(on b1 b9)
(on b3 b1)
(on b4 b10)
(on b5 b3)
(on b6 b7)
(on b7 b8)
(on b9 b6)
(on b10 b5))
)
)


