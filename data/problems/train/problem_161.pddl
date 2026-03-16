

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b10)
(ontable b4)
(on b5 b11)
(on b6 b1)
(on b7 b12)
(on b8 b4)
(on b9 b6)
(on b10 b9)
(ontable b11)
(on b12 b2)
(clear b3)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b9)
(on b3 b5)
(on b5 b12)
(on b6 b10)
(on b7 b4)
(on b8 b7)
(on b9 b1)
(on b11 b6))
)
)


