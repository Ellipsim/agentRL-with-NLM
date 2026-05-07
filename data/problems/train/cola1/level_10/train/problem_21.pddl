

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b12)
(ontable b2)
(on b3 b7)
(on b4 b11)
(on b5 b2)
(on b6 b3)
(on b7 b4)
(on b8 b5)
(on b9 b10)
(on b10 b6)
(ontable b11)
(ontable b12)
(clear b1)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b5)
(on b3 b12)
(on b5 b10)
(on b6 b7)
(on b7 b9)
(on b9 b3)
(on b10 b11)
(on b11 b8)
(on b12 b1))
)
)


