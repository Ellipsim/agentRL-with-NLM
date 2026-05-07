

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b10)
(on b3 b1)
(on b4 b9)
(on b5 b11)
(ontable b6)
(on b7 b8)
(on b8 b3)
(ontable b9)
(ontable b10)
(on b11 b2)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b11)
(on b3 b1)
(on b5 b8)
(on b6 b3)
(on b7 b9)
(on b9 b4)
(on b10 b6)
(on b11 b5))
)
)


