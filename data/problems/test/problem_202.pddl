

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b7)
(on b4 b5)
(on b5 b2)
(on b6 b4)
(on b7 b1)
(on b8 b3)
(ontable b9)
(on b10 b9)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b3 b10)
(on b5 b6)
(on b7 b1)
(on b8 b9)
(on b9 b3)
(on b10 b5))
)
)


